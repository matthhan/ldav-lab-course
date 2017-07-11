package edu.ldav.prefixspan

object PrefixSpan {
  type Item = Int
  type SequentialPattern = Seq[Item]
  case class PatternWithFrequency(pattern: SequentialPattern,frequency: Int)
  case class PatternWithBadness(pattern: SequentialPattern,badness: Double)
  def prefixSpan(sequenceDatabase:Seq[Seq[String]],minSupport:Int):(Seq[PatternWithBadness],TwoWayDictionary) = {
    /*
     * First replace every item by a unique int so that comparisons are fast
     */
    val allItemStrings = sequenceDatabase.flatten.distinct
    System.err.println("1")
    val dictionary = new TwoWayDictionary(allItemStrings)
    System.err.println("2")
    val allItems = allItemStrings.map(dictionary.indexOfString)
    System.err.println("3")
    val simplifiedSequenceDatabase = sequenceDatabase.map(sequence => sequence.map(dictionary.indexOfString))

    System.err.println("done making sequence database")

    var i:Int = 1
    /*
     * Define a recursion to do the actual prefixSpan calculation
     */
    def prefixSpanRecursion(currentSequence:SequentialPattern,db:Seq[Seq[Item]]): Seq[PatternWithFrequency] = {
      if(currentSequence.length == 1) {
        i = i+1
        System.err.println(s"Expanding the $i -th sequential pattern ${currentSequence}")
      }
      val newPatterns = allItems.map(item => (item,frequencyIn(db).apply(item)))
                              .filter(_._2 >= minSupport)
                              .map(t => PatternWithFrequency(currentSequence :+ t._1 ,t._2))
      System.err.println(s"created ${newPatterns.length} new patterns`")
      newPatterns ++ newPatterns.flatMap(p => prefixSpanRecursion(p.pattern, projectedDatabase(db, p.pattern.last)))
    }
    (prefixSpanRecursion(Seq[Item](),simplifiedSequenceDatabase).map(calcBadness),dictionary)
  }
  private def frequencyIn(db:Seq[Seq[Item]]): (Item => Int) = {
      item:Item => db.par.count(_.startsWith(Seq(item)))
  }
  private def projectedDatabase(db:Seq[Seq[Item]],item:Item):Seq[Seq[Item]] = {
    System.err.println(s"Finding projected Database of ${item}")
    db.par.map(afterFirstOccurrenceOf(item)).filter(_.nonEmpty).seq
  }
  private def afterFirstOccurrenceOf(item: Item) = {
    sequence:Seq[Item] => if(sequence.startsWith(Seq(item))) sequence.tail else Seq()
  }
  private def calcBadness(s:PatternWithFrequency):PatternWithBadness = PatternWithBadness(s.pattern,Math.pow(s.frequency , s.pattern.length))
}
