variable "region" {
  type = string
  description = "AWS Region"
}

variable "profile" {
    type = string
    description = "AWS IAM Profile to execute commands" 
}

variable "allow_ssh_from_ip" {
    type = string
    description = "From IP in inboudn rule"  
}

variable "ssh_port" {
  type = number
  description = "TCP port that allows SSH"
}

variable "transport_protocol" {
  type = string
  description = "Transport protocol used by ssh"
}

variable "allow_all_outbound" {
  type = string
  description = "Allow all outbound Traffic for EC2 instances"
  default = "0.0.0.0/0"
}

variable "allow_all_protocol" {
  type = string
  default = "-1"
}

variable "ami" {
    type = string
    description = "AMI"  
}

variable "instance_type" {
    type = string
    description = "Instance Type of EC2"  
}

variable "tags" {
    type = map(string)
}

variable "key_name" {
    type = string
    description = "The Name of the ssh Key"
}