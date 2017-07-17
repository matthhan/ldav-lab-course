import data from './data.json';
import includes from 'lodash';

const courses = Object.keys(data)
export default class Data {
  getCourses() {
    return courses.filter(course => data[course].accesses.length > 0 );
  }
  getDataForCourse(course) {
    if(!course) return undefined
    if(includes(this.getCourses(),course)) return data[course].accesses;
    else return undefined
  }
  getSemester(course) {
    return data[course].semester
  }
  getFaculty(course) {
    return data[course].faculty
  }
  getTitle(course) {
    return data[course].title
  }
  getInstitute(course) {
    return data[course].institute
  }
}
