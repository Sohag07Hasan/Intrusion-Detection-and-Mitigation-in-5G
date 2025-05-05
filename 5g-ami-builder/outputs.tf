output "builder_pubip" {
    value = resource.aws_instance.builder.public_ip
}