package edu.ldav.prefixspan

import scala.io.Source

object Main extends App {
  val res = PrefixSpan.prefixSpan(Source.fromFile("sessions.csv").getLines().map(_.split(",").toSeq).toSeq)
  print(res.take(5))
}
