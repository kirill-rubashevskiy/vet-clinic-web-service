# Vet Clinic FastAPI Web Service:dog2::hospital: 

The FastAPI web service for a vet clinic, developed as a DevOps course assignment during study at [HSE University Master’s Programme Machine Learning and Data-Intensive Systems](https://www.hse.ru/en/ma/mlds/).

## Task

Create and deploy the FastAPI web service for a vet clinic to store and update the information about its patients according to [the provided OpenAPI documentation](clinic.yaml).

## Usage

The service is deployed on render.com and available at https://vet-clinic-web-service.onrender.com/ (it may take it a minute or two to turn on). Please refer to the [service documentation](https://vet-clinic-web-service.onrender.com/docs) for the available operations.

If you want to run the service locally: 

1. clone the repository 
2. in Terminal run command `docker-compose up -d`

## Versions

- **v1.0**: the service is built and deployed according to the initial assignment
- **v1.1**: added PostgresSQL support to store the service database
- **v1.2**: the app containerized with Docker