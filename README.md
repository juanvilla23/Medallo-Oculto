# **Medallo Oculto**

## Router Machines Configuration

In the `resources/data` directory, you can find two subdirectories where you need to configure the necessary data for routing in the application. We use [OSRM](https://project-osrm.org/), and each subdirectory, **car_profile** and **foot_profile**, represents the two travel modes in the application. Each one has instructions for processing the data for the specified profile. We use an instance of the **osrm/osrm-backend** Docker image to run the corresponding profile. Below, you can see a generic instruction. You can find more information about **osrm/osrm-backend** on [DockerHub](https://hub.docker.com/r/osrm/osrm-backend).

1. You need to download the data. We use data from [Geofabrik](https://download.geofabrik.de/), specifically data about Colombia, which is our reference point. Example: `wget https://download.geofabrik.de/south-america/colombia-latest.osm.pbf`.

2. The next step is to preprocess the data with the selected profile. Example: `docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/colombia-latest.osm.pbf`. You need to run this command in the directory where the file with the `osm.pbf` extension is located. In the **/opt/car.lua** part, **car** is the selected profile, but you can change this to select another profile, for example, **foot** for pedestrian routes.

3. We need to continue with the preprocessing using the commands `docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/colombia-latest.osrm` and `docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/colombia-latest.osrm`. If you complete this step, you will have the necessary data to run the `docker-compose` file.

## How to Run the Project

1. First, you need to clone the project from the repository and configure the **.env** file. We have a template on how to do this in **.env_template** with the instructions.

2. You need to have the Docker daemon running and bring up the `docker-compose` with `docker compose up -d`.

3. Make the respective project migrations with `python manage.py migrate && python manage.py makemigrations`.

4. Finally, you can run the Django application with `python manage.py runserver`.


