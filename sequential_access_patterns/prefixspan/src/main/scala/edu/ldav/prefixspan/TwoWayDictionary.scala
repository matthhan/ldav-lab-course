package edu.ldav.prefixspan

class TwoWayDictionary(items:Seq[String]) {
  System.err.println("making TwoWayDictionary")
  private val thereDir = items.toArray
  System.err.println("Made array")
  private val backdir = scala.collection.mutable.HashMap[String,Int]()
  private def initBackdirection() = {
    System.err.println("making dictionary")
    System.err.print(".")
    thereDir.indices.foreach(i => this.backdir.put(thereDir(i),i))
  }
  this.initBackdirection()
  def indexOfString(s:String): Int = this.backdir(s)
  def stringOfIndex(i:Int): String = this.thereDir(i)
}
