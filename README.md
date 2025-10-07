# Odoo Development Learning

This repository contains a Docker-based setup for learning Odoo development.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository
2. Start the Odoo and PostgreSQL services:

```bash
docker-compose up -d
```

3. Access Odoo at: http://localhost:8069

4. Default credentials:
   - Database: postgres
   - Master Password: admin
   - Username: admin (after creating a database)
   - Password: admin (set during database creation)

## Services

- **web**: Odoo 17.0 application server (port 8069)
- **db**: PostgreSQL 15 database server

## Directory Structure

- `config/`: Odoo configuration files
- `addons/`: Custom Odoo addons/modules
- `odoo-web-data`: Docker volume for Odoo data
- `odoo-db-data`: Docker volume for PostgreSQL data

## Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web
docker-compose logs -f db

# Restart services
docker-compose restart

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose down -v
```

## Troubleshooting

If you encounter database connection issues:

1. Ensure both services are running: `docker-compose ps`
2. Check the logs: `docker-compose logs`
3. Restart the services: `docker-compose restart`

## Development

Place your custom Odoo modules in the `addons/` directory. They will be automatically available in Odoo.
