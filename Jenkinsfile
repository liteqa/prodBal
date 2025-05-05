pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('Prod_Wall_Bal') {
      steps {
        python3 -m venv venv
        source venv/bin/activate
        pip install requests
        sh 'python3 Prod_Wall_Bal.py'
      }
    }
  }
}
