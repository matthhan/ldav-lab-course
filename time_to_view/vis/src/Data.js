import data from './data.json';

const courses = 
  Object.keys(data)
    .filter(course => Object.keys(data[course]).length > 1)
    .filter(course => data[course][Object.keys(data[course])[0]].accesses.length > 1);
export default class Data {
  getCourses() {
    return courses;
  }
  getDocumentsForCourse(course) {
    return Object.keys(data[course]);
  }
  getDataForDocument(course,document) {
    return data[course][document];
  }
}
