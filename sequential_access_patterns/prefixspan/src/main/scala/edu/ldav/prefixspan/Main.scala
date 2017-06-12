package edu.ldav.prefixspan

import scala.io.Source

object Main {
  def main(args:Array[String]) = {
    val db = Source.fromFile(args(0)).getLines().map(_.split(",").toSeq).toSeq
    val (res,dict) = PrefixSpan.prefixSpan(db,args(1).toInt)
    res.sortBy(_.frequency)
    print("[")
    res.map(pattern =>
      "{" + enquote("badness") + ":" + pattern.frequency + "," +
        enquote("pattern") + ":[" + pattern.pattern.map(i => enquote(dict.stringOfIndex(i))).mkString(",") +
        "]}")
      .foreach(x => print(x + ",\n"))
    print("]")
  }
  def enquote(s:String)= "\"" + s + "\""
}
