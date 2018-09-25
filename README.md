# Pytorch Super resolution NN in a NodeJS service 
NodeJS server for super resolution CNN inference

# Build Image
`docker-compose up`

# Run
`docker run --user 1001 -p 8888:8000 -it --entrypoint=/bin/bash dl_docker -i`

# Copy files
`docker cp assets\models\superres\model_epoch_150.pth dl_docker:/app/assets/models/superres/model_epoch_150.pth`
