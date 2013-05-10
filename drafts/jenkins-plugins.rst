==========================
 Writing a Jenkins Plugin
==========================
:date: 2013-05-09 
:category: programming
:tags: jenkins,plugin
:author: Yusuke Tsutsumi

Writing plugins for `Jenkins <http://jenkins-ci.org/>`_ can be considered a rite of passage for those working deep in build code: it can be a ride of trials, tribulations, and of strange languages you've never heard before. Here's a small introduction to the large world of developing for Jenkins.

**NOTE**: This is for Linux/Unix (OS X) based instructions! Things can change for other operating systems!

Getting Set Up
==============

Java
----

Jenkins uses Java. Download either the `OpenJDK <http://openjdk.java.net/>`_ or the `Sun JDK <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`_. I would suggest googling install instructions if it isn't listed for your particular operating system.

Maven
-----

The first thing you'll need beyond anything is Maven 3. If you're not familiar with it, Maven 3 is the standard dependency management and build tool for Java services. You can download Maven here: `Maven <http://maven.apache.org/download.cgi>`_.

You'll need to extract the Maven 3 executable (mvn) and add it to your  path, or call it explicitely. 

Your M2 File
------------

You'll also need to copy some info into your m2 file, which stores the configuration for Maven. You can copy it from the `Jenkins Plugin Tutorial Page  <https://wiki.jenkins-ci.org/display/JENKINS/Plugin+tutorial>`_, or the less-maintained snippet below: 
    <settings>
      <pluginGroups>
        <pluginGroup>org.jenkins-ci.tools</pluginGroup>
      </pluginGroups>

      <profiles>
        <!-- Give access to Jenkins plugins -->
        <profile>
          <id>jenkins</id>
          <activation>
            <activeByDefault>true</activeByDefault> <!-- change this to     false, if you don't like to have it on per default -->
          </activation>
          <repositories>
            <repository>
              <id>repo.jenkins-ci.org</id>
              <url>http://repo.jenkins-ci.org/public/</url>
            </repository>
          </repositories>
          <pluginRepositories>
            <pluginRepository>
              <id>repo.jenkins-ci.org</id>
              <url>http://repo.jenkins-ci.org/public/</url>
            </pluginRepository>
          </pluginRepositories>
        </profile>
      </profiles>
      <mirrors>
        <mirror>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
          <mirrorOf>m.g.o-public</mirrorOf>
        </mirror>
      </mirrors>
    </settings>

This configuration adds the jenkins mirror as a valid location to download dependencies, giving Maven (and you) access to all of the tools and dependencies you need to create Jenkins plugins.

Creating the plugin
===================
Maven has been extended to provides the ability to create Jenkins plugins. There are other methods, but this my preferred methodology:

    mvn -U org.jenkins-ci.tools:maven-hpi-plugin:create

You'll be asked a few questions regarding your new plugin. Here's a short description of each:

* groupID: this is the namespace your plugin will be added to. I'd suggest the default, or org.jenkins-ci.plugins.
* artifactID: this is a unique name for your plugin. Don't add 'plugin' in the name - that's already clear from the groupID. Just use 'helloWorld' or 'tmkTut' if you don't have a plugin in mind.

After this is done, congratulations! you've just created the bare minimum needed for a Jenkins plugin. It does absolutely nothing except for being installable and printing a 'Hello World' to the logs after your build.

The files
---------

You can skip this part if you want. Just wanted to briefly describe each of these files.

Your file tree should look something like this:


    ├── pom.xml
    └── src
        └── main
            ├── java
            │   └── org
            │       └── jenkins
            │           └── tmkTut
            │               └── HelloWorldBuilder.java
            └── resources
                ├── index.jelly
                └── org
                    └── jenkins
                        └── tmkTut
                            └── HelloWorldBuilder
                                ├── config.jelly
                                ├── global.jelly
                                ├── help-name.html
                                └── help-useFrench.html

* pom.xml: poms are Maven's configuration for building a specific Java package. It contains information about the version of the package, as well as the groupId and artifactID you filled out earlier.
build process of a Job. 
* HelloWorldBuilder.java: this is the main class of your plugin. Note that it extends off of the 'Builder' class in Jenkins. As the documentation within the file describes, this handles the creating and configuration of your plugin. In this case, it's 'HelloWorldBuilder'
* index.jelly: this is what will be show to admins who look at the plugin under 'available plugins' and 'installed plugins'. It should be a short description of what your plugin is, and what it does.
* config.jelly: Note here that these are contained under a 'HelloWorldBuilder' folder. This means this file is specifically related to that class. The config.jelly describes what the configuration block looks like for your plugin (or that particular class)
* global.jelly