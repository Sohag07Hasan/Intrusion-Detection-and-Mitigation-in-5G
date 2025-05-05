
variable "vpc_cidr" {
  type = string
  description = "VPC CIDR"
}

variable "subnet_cidr" {
  type = string
  description = "Subnet CIDR"
}


variable "tags" {
    type = map(string)
    description = "Tags"
    default = {
        "project": "5g-cloud-testbed"
        "creator" = "Mahibul"
    }
}


variable "ami" {
  type = string
  description = "Region specific AMI"
}

variable "instance_type" {
  type = string
  description = "Region specific AMI"
}

variable "key_pair" {
  type = string
  description = "Key Pair Name"  
}
