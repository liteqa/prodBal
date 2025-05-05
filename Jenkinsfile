pipeline {
    agent any

    stages {
        stage('Setup Python Environment & Run Script') {
            steps {
                // Checkout your code from SCM automatically (configured in Jenkins)
                checkout scm
                
                // Run shell commands
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install requests urllib3 PrettyTable pandas xlrd
                    python Prod_Wall_Bal.py
                '''
            }
        }
    }
}
