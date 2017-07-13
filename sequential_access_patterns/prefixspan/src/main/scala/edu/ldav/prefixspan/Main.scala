package edu.ldav.prefixspan

import scala.io.Source

object Main {
  def main(args:Array[String]) = {
    val db = Source.fromFile(args(0)).getLines().map(_.split(",").toSeq).toSeq
    val (res,dict) = PrefixSpan.prefixSpan(db,args(1).toInt)
    System.err.println("done with calculation. outputting")
    val sorted = res.sortBy(-_.badness)
    print("[")
    sorted.map(pattern =>
      "{" + enquote("badness") + ":" + pattern.badness + "," +
        enquote("pattern") + ":[" + pattern.pattern.map(i => enquote(dict.stringOfIndex(i))).mkString(",") +
        "]}")
          .zipWithIndex.foreach( { case (x,i) => print(x + (if(i < sorted.length -1) ",\n" else  "")) } )
    print("]")
  }
  def enquote(s:String)= "\"" + s + "\""
}
