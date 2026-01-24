terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = "de-zoomcamp-2026-485107"
  region      = "us-central1"
}

