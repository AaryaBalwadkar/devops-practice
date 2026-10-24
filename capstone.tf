terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "capstone_env" {
  filename = "${path.module}/capstone.env"
  content  = "PAYMENT_GATEWAY_URL=http://localhost:30099\nSTATUS=DEPLOYED\n"
}
