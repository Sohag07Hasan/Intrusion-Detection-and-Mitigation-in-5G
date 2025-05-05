region = "us-east-1"

profile = "terraform" #credentails stored in ~./aws/

instance_type = "t2.micro" #free tier

allow_ssh_from_ip = "0.0.0.0/0" # From Any IP

ssh_port = 22

transport_protocol = "tcp"

ami = "ami-084568db4383264d4" #Ubuntu 24.04 (64-bit x86) ami is region dependednt

key_name = "5g_tb"

tags = {
  "creator" = "Mahibul"
  "name"    = "5g-ami-builder"
  "project" = "5g-cloud-testbed"
}