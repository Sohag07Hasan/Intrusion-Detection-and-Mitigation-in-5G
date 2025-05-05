
#Create VPC, subnet, and EC2 instance per region
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr
  tags       = var.tags
}

resource "aws_subnet" "subnet" {
  vpc_id                  = aws_vpc.vpc.id
  map_public_ip_on_launch = true
  cidr_block              = var.subnet_cidr
  tags                    = var.tags
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags   = var.tags
}

resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_main_route_table_association" "rta" {
  vpc_id         = aws_vpc.vpc.id
  route_table_id = aws_route_table.rt.id
}

resource "aws_security_group" "sg" {
  name        = "allow-all"
  description = "Allow All Traffic"
  vpc_id      = aws_vpc.vpc.id
  tags        = var.tags
}

resource "aws_vpc_security_group_ingress_rule" "ingress_all" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = -1 #all protocol and all ports
}

resource "aws_vpc_security_group_egress_rule" "egress_all" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = -1 #all protocol and all ports
}

resource "aws_instance" "ec2" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.subnet.id
  vpc_security_group_ids      = [aws_security_group.sg.id]
  key_name                    = var.key_pair
  associate_public_ip_address = true
  tags                        = var.tags
}
