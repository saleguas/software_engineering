docker build -t buildimage .
docker run -d -p 5000:5000 buildimage:latest