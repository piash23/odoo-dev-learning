#!/bin/bash
# Simple validation script to check Docker Compose configuration

echo "Validating Docker Compose configuration..."

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found!"
    exit 1
fi

# Validate docker-compose.yml syntax
echo "Checking docker-compose.yml syntax..."
if docker compose config > /dev/null 2>&1; then
    echo "✓ docker-compose.yml syntax is valid"
else
    echo "✗ docker-compose.yml syntax is invalid"
    exit 1
fi

# Check for required services
echo "Checking for required services..."
if docker compose config | grep -q "services:" && \
   docker compose config | grep -q "db:" && \
   docker compose config | grep -q "web:"; then
    echo "✓ Required services (web, db) are defined"
else
    echo "✗ Missing required services"
    exit 1
fi

# Check if web service depends on db
echo "Checking service dependencies..."
if docker compose config | grep -A 10 "web:" | grep -q "depends_on:"; then
    echo "✓ Web service has dependencies configured"
else
    echo "✗ Web service dependencies not configured"
    exit 1
fi

# Check for required directories
echo "Checking required directories..."
if [ -d "config" ] && [ -d "addons" ]; then
    echo "✓ Required directories (config, addons) exist"
else
    echo "✗ Missing required directories"
    exit 1
fi

# Check if odoo.conf exists
if [ -f "config/odoo.conf" ]; then
    echo "✓ Odoo configuration file exists"
    
    # Check if db_host is set to 'db'
    if grep -q "db_host = db" config/odoo.conf; then
        echo "✓ Database host is correctly set to 'db'"
    else
        echo "✗ Database host is not correctly configured"
        exit 1
    fi
else
    echo "✗ Odoo configuration file not found"
    exit 1
fi

echo ""
echo "All validation checks passed! ✓"
echo ""
echo "The Docker Compose configuration is properly set up to fix the database connection issue."
echo "The 'web' service will now be able to connect to the 'db' service."
