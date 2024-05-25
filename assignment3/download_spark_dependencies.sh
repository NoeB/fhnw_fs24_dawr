#!/bin/bash

# Set the desired versions
HADOOP_AWS_VERSION="3.4.0"
AWS_JAVA_SDK_VERSION="1.12.724"

# Set the directory to store the downloaded JARs
JAR_DIRECTORY="./jars"

# Create the directory if it doesn't exist
mkdir -p "$JAR_DIRECTORY"

# Download the Hadoop AWS JAR
wget -P "$JAR_DIRECTORY" "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/$HADOOP_AWS_VERSION/hadoop-aws-$HADOOP_AWS_VERSION.jar"

# Download the AWS Java SDK JAR
wget -P "$JAR_DIRECTORY" "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/$AWS_JAVA_SDK_VERSION/aws-java-sdk-bundle-$AWS_JAVA_SDK_VERSION.jar"

echo "JAR files downloaded successfully."