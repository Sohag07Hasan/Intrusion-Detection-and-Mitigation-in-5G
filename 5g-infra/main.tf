terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.97.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  alias  = "region_1"
}

provider "aws" {
  region = "us-west-1"
  alias  = "region_2"
}


#Instance Created at US East
module "us_east" {
  source        = "./modules/region_resources"
  providers     = { aws = aws.region_1 }
  key_pair      = "5g_tb"
  subnet_cidr   = "10.10.1.0/24"
  ami           = "ami-084568db4383264d4" #"ami-0c87495d330148ddc"
  vpc_cidr      = "10.10.0.0/16"
  instance_type = "t2.micro"
}

#Instance Crated at US West
module "us_west" {
  source        = "./modules/region_resources"
  providers     = { aws = aws.region_2 }
  key_pair      = "5g_tb"
  subnet_cidr   = "10.20.1.0/24"
  ami           = "ami-04f7a54071e74f488" #"ami-04e278da5cb8c86a0"
  vpc_cidr      = "10.20.0.0/16"
  instance_type = "t2.micro"
}

