terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.97.0"
    }
  }
}

provider "aws" {
  region = var.region
  profile = var.profile
}

#to use default vpc
data "aws_vpc" "default" {
  default = true
}

#create a new security group
resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = data.aws_vpc.default.id
  tags = var.tags
}

#allow inbound ssh
resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.allow_tls.id
  cidr_ipv4         = var.allow_ssh_from_ip
  from_port         = var.ssh_port
  ip_protocol       = var.transport_protocol
  to_port           = var.ssh_port
}

#allow outbound all traffic ssh
resource "aws_vpc_security_group_egress_rule" "allow_outbound" {
  security_group_id = aws_security_group.allow_tls.id
  cidr_ipv4         = var.allow_all_outbound
  ip_protocol       = var.allow_all_protocol
}


#aws instance
resource "aws_instance" "builder" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = var.key_name
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.allow_tls.id]
  tags                        = var.tags
}

