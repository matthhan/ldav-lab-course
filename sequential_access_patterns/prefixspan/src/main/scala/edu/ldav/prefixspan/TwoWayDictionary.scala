package edu.ldav.prefixspan

class TwoWayDictionary(items:Seq[String]) {
  private val thereDir = items.toArray

  private def initBackdirection = {
    var temp = Map[String,Int]()
    thereDir.indices.foreach(i => {temp = temp.updated(items(i),i)})
    temp
  }

  private val backdir = initBackdirection
  def indexOfString(s:String): Int = this.backdir(s)
  def stringOfIndex(i:Int): String = this.thereDir(i)
}
