package edu.ldav.prefixspan

object PrefixSpan {
  type Item = Int
  type SequentialPattern = Seq[Item]
  case class PatternWithFrequency(pattern: SequentialPattern,frequency: Int)
  def prefixSpan(sequenceDatabase:Seq[Seq[String]],minSupport:Int):(Seq[PatternWithFrequency],TwoWayDictionary) = {
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
      val newPatterns = allItems.map(item => (item,frequencyIn(db).apply(item)))
                              .filter(_._2 >= minSupport)
                              .map(t => PatternWithFrequency(currentSequence :+ t._1 ,t._2))
      newPatterns ++ newPatterns.flatMap(p => prefixSpanRecursion(p.pattern, projectedDatabase(db, p.pattern.last)))
    }
    (prefixSpanRecursion(Seq[Item](),simplifiedSequenceDatabase),dictionary)
  }
  private def frequencyIn(db:Seq[Seq[Item]]): (Item => Int) = {
    item:Item => db.par.count(_.contains(item))
  }
  private def projectedDatabase(db:Seq[Seq[Item]],item:Item):Seq[Seq[Item]] = {
    db.par.map(afterFirstOccurrenceOf(item)).filter(_.nonEmpty).seq
  }
  private def afterFirstOccurrenceOf(item: Item) = {
    sequence:Seq[Item] =>  sequence.slice(sequence.indexOf(item)+1,sequence.length -1)
  }
}
