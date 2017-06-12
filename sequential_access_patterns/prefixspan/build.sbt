import Dependencies._

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "edu.ldav",
      scalaVersion := "2.11.8",
      version      := "0.1.0"
    )),
    name := "PrefixSpan",
    libraryDependencies += scalaTest % Test
  )
