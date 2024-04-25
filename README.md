# snippy-converter
Snippy Converter is a user-friendly Flask web application designed to streamline the conversion process from PDF to DOCX format. With its intuitive interface and efficient backend processing, users can effortlessly transform their PDF documents into editable DOCX files with just a few clicks.

<h2>Features</h2>
<ul>
  <li>PDF to DOCX Conversion: Easily convert PDF documents to DOCX. </li>
  <li>User-Friendly Interface: Simple and easy-to-use interface.</li>
  <li>Efficient Processing: Quick and accurate conversion.</li>
  <li>Error Handling: Clear feedback for any issues.</li>
  <li>Responsive Design: Works well on different devices.</li>
</ul>

<h2>Prerequisites</h2>
<ul>
  <li>AWS Account.</li>
 <li>Programmatic access and AWS configured with CLI.</li>
 <li>Python3 Installed.</li>
 <li>Docker and Kubectl installed.</li>
 <li>Code editor (Vscode)</li>
</ul>

<h2>✨Let’s Start the Project ✨</h2>
<h2>Part 1 : Deploying the Flask application locally</h2>

step 1 : Clone the repository
```bash
git clone <repository_url>
```
Step 2: Install dependencies
```bash
pip3 install -r requirements.txt
```
Step 3: Run the application
```bash
python3 app.py
```

<h2>Part 2 : Dockerizing the Flask application</h2>
<h3>step 1 : Clone the repository</h3>

```bash
# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set the environment variables for the Flask app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["flask", "run"]

```

<h3>Step 2: Build the Docker image</h3>
<p>To build the Docker image, execute the following command:</p>

```bash
docker build -t <image_name> .

```
<h3>Step 3: Run the Docker container</h3>
<p>To run the Docker container, execute the following command:</p>

```bash
docker run -p 5000:5000 <image_name>
```
<p>This will start the Flask server in a Docker container on localhost:5000. Navigate to http://localhost:5000/ on your browser to access the application.</p>


<h2>Part 3: Pushing the Docker image to ECR</h2>
<h3>Step 1: Create an ECR repository</h3>
<p>Create an ECR repository using Python: </p>

```bash
import boto3

# Create an ECR client
ecr_client = boto3.client('ecr')

# Create a new ECR repository
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)

# Print the repository URI
repository_uri = response['repository']['repositoryUri']
print(repository_uri)

```

<h3>Step 2: Push the Docker image to ECR</h3>
<p>Push the Docker image to ECR using the push commands on the console:</p>

```bash
docker push <ecr_repo_uri>:<tag>

```

<h2>Part 4: Creating an EKS cluster and deploying the app using Python</h2>
<h3>Step 1: Create an EKS cluster
</h3>
<p>Create an EKS cluster and add node group
</p>

<h3>Step 2: Create a node group
</h3>
<p>Create a node group in the EKS cluster.

</p>

<h3>Step 3: Create deployment and service
</h3>

```bash
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my-cloud-native-repo:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)


```
<p>make sure to edit the name of the image on line 25 with your image Uri.</p>
<ul>
  <li>Once you run this file by running “python3 eks.py” deployment and service will be created.
</li>
  <li>Check by running following commands:
</li>
</ul>

```
kubectl get deployment -n default (check deployments)
kubectl get service -n default (check service)
kubectl get pods -n default (to check the pods)

```
<p>Once your pod is up and running, run the port-forward to expose the service</p>

```
kubectl port-forward service/<service_name> 5000:5000

```
