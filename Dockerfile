FROM python:3.6-slim

ENV WEATHER_API_KEY=e562561c836c9376d3a90f7af388195e

# copy the requirements file into the image
COPY ./requirements.txt /sales_pipeline/requirements.txt

# switch working directory
WORKDIR /sales_pipeline

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY /src ./src
COPY /data ./data
COPY /configs ./configs


# configure the container to run in an executed manner
CMD ["python", "src/main.py"]