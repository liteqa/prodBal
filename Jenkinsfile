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
        sh 'python3 Prod_Wall_Bal.py'
      }
    }
  }
}
