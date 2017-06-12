package edu.ldav.prefixspan

object PrefixSpan {
  val minSupport = 30
  type Item = Int
  type SequentialPattern = Seq[Item]
  case class PatternWithFrequency(pattern: SequentialPattern,frequency: Int)
  def prefixSpan(sequenceDatabase:Seq[Seq[String]]):Seq[PatternWithFrequency] = {
    /*
     * First replace every item by a unique int so that comparisons are fast
     */
    val allItemStrings = sequenceDatabase.flatten.distinct
    val dictionary = new TwoWayDictionary(allItemStrings)
    val allItems = allItemStrings.map(dictionary.indexOfString)
    val simplifiedSequenceDatabase = sequenceDatabase.map(sequence => sequence.map(dictionary.indexOfString))

    /*
     * Define a recursion to do the actual prefixSpan calculation
     */
    def prefixSpanRecursion(currentSequence:SequentialPattern,db:Seq[Seq[Item]]): Seq[PatternWithFrequency] = {
      val newPatterns = allItems.par.map(item => (item,frequencyIn(db).apply(item)))
                              .map(t => PatternWithFrequency(currentSequence :+ t._1 ,t._2))
                              .filter(_.frequency >= minSupport).seq
      newPatterns ++ newPatterns.par.flatMap(p => prefixSpanRecursion(p.pattern, projectedDatabase(db, p.pattern.last))).seq
    }
    prefixSpanRecursion(Seq[Item](),simplifiedSequenceDatabase)
  }
  private def frequencyIn(db:Seq[Seq[Item]]): (Item => Int) = {
    item:Item => db.count(_.contains(item))
  }
  private def projectedDatabase(db:Seq[Seq[Item]],item:Item):Seq[Seq[Item]] = {
    db.par.map(afterFirstOccurrenceOf(item)).filter(_.nonEmpty).seq
  }
  private def afterFirstOccurrenceOf(item: Item) = {
    sequence:Seq[Item] =>  sequence.slice(sequence.indexOf(item),sequence.length -1)
  }
}
