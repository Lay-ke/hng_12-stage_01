pipeline {
    agent any

    stages {
        stage('Pulling code from GitHub') {
            steps {
                git branch: 'main', url: 'https://github.com/Lay-ke/hng_12-stage_01'
            }
        }

        stage('Building code') {
            steps {
                sh '''
                    echo "Building the code"
                    docker build -t number-classifier-app .
                    docker image ls
                    docker tag number-classifier-app:latest mintah/number-classifier-app:latest
                '''
            }
        }

        stage('Testing') {
            steps {
                script {
                    echo "Running tests"
                    sh 'docker stop number-classifier-app || true'
                    sh 'docker run -d -p 80:80 --name number-classifier-app mintah/number-classifier-app:latest'
                    // Wait for the application to be ready (adjust sleep time as necessary)
                    sh 'sleep 10'

                    // Run a GET request to the classify-number route
                    def response = sh(script: 'curl -s -o response.txt -w "%{http_code}" "http://localhost/api/classify-number?number=153"', returnStdout: true).trim()

                    // Read the response code and content (can be expanded for detailed checks)
                    def statusCode = response[-3..-1]
                    def responseContent = readFile('response.txt').trim()

                    echo "Response Status Code: ${statusCode}"
                    echo "Response Body: ${responseContent}"

                    // Verify that the status code is 200 (OK)
                    if (statusCode != '200') {
                        error "API test failed: Status code ${statusCode}"
                    }                
                }
                
            }
        }

        stage('Publishing to docker hub') {
            steps {
                sh 'echo "Publishing the image to Docker Hub"'
                withDockerRegistry([credentialsId: 'docker-credentials', url: 'https://index.docker.io/v1/']) {
                    sh 'docker push mintah/number-classifier-app:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ssh_credentials', keyFileVariable: 'PRIVATE_KEY_PATH', usernameVariable: 'EC2_USER')]) {
                    script {
                       echo "Deploying to EC2 instance"
                       // The private key and username are now available as environment variables
                       echo "Using EC2 user: \$EC2_USER"
                       echo "Private key path: \$PRIVATE_KEY_PATH"
                       // EC2 host (replace with your actual EC2 public IP)
                       EC2_HOST="3.252.138.182"  
                       // Now you can use the SSH key and username in the SSH command
                       sh """
                           echo "Inside EC2 instance. Starting deployment..."
                           ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i \$PRIVATE_KEY_PATH \$EC2_USER@$EC2_HOST << 'EOF'
                               echo "Deployment started..."
                               docker pull mintah/number-classifier-app:latest
                               if docker ps -q --filter "name=number-classifier-app"; then
                                docker stop number-classifier-app || true
                                docker rm number-classifier-app || true
                               fi
                               docker ps --filter "name=number-classifier-app" -q && docker stop number-classifier-app || true
                               docker ps -a --filter "name=number-classifier-app" -q && docker rm number-classifier-app || true
                               docker run -d -p 80:80 --name number-classifier-app mintah/number-classifier-app:latest
                               echo "Deployment complete"
                           EOF
                       """
                    }
                }
            }
        }
    }
}