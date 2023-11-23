import boto3
import json

def lambda_handler(event, context):
    master_id = "i-0ed35a18893e4e8c5"  # ASAvOne instance ID
    ec2_re = boto3.resource("ec2", 'eu-west-2')
    ec2_cli = boto3.client("ec2", 'eu-west-2')
    primary_instance = ec2_re.Instance(master_id)

    # ------------ Available but not used -------------------
    # slave_id = "i-05cdb109f20b48997"  # ASAvTwo Instance ID
    # sns_client=boto3.client("sns",'eu-west-2')
    # secondary_instance = ec2_re.Instance(slave_id)
    # response_IP = ec2_cli.describe_addresses()

    if primary_instance.state['Name'] != "running":
        print("Primary ASA gone down, Deleted 3.10.245.197 from Primary ASA and Attached 3.10.245.197 in Secondary ASA")

        # -------------Replace the Route of 172.31.128.0/24 --------------
        Replace_route_172_31_128_0 = ec2_cli.replace_route(
            DestinationCidrBlock='172.31.128.0/24',  # CIDR for Client Assigned IP's
            NetworkInterfaceId='eni-04099ea4d478df814',  # inside interfce on ASAvTwo
            RouteTableId='rtb-0d6253afbd5268fb1')  # main RT

        # -------------Replace the Route of 172.31.129.0/24 --------------
        Replace_route_172_31_129_0 = ec2_cli.replace_route(
            DestinationCidrBlock='172.31.129.0/24',  # CIDR for Client Assigned IP's
            NetworkInterfaceId='eni-04099ea4d478df814',  # inside interfce on ASAvTwo
            RouteTableId='rtb-0d6253afbd5268fb1')  # main RT

        # -------------Replace the Route of 172.31.130.0/23 --------------
        Replace_route_172_31_130_0 = ec2_cli.replace_route(
            DestinationCidrBlock='172.31.130.0/23',  # CIDR for Client Assigned IP's
            NetworkInterfaceId='eni-04099ea4d478df814',  # inside interfce on ASAvTwo
            RouteTableId='rtb-0d6253afbd5268fb1')  # main RT

        # -------------Replace the Route of 172.31.252.0/23 --------------
        Replace_route_172_31_252_0 = ec2_cli.replace_route(
            DestinationCidrBlock='172.31.252.0/23',  # CIDR for Client Assigned IP's
            NetworkInterfaceId='eni-04099ea4d478df814',  # inside interfce on ASAvTwo
            RouteTableId='rtb-0d6253afbd5268fb1')  # main RT

        # ---------------DisassociateIP----------------
        disassociateIP_response_Primary = ec2_cli.disassociate_address(
            PublicIp='3.10.245.197')

        # ------------------AssociateIP---------------------------------------
        AssociateIP_response_Secondary = ec2_cli.associate_address(
            AllocationId='eipalloc-0d684af2afccff218',  # ASAvOne ASAvExternalIp
            NetworkInterfaceId='eni-045d87815d166d152')  # outside interface on ASAvTwo

    else:
        print("Primary ASA is running")
    return None
