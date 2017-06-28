import data from './data.json';

const courses = Object.keys(data);
export default class Data {
  getCourses() {
    return courses;
  }
  getDocumentsForCourse(course) {
    console.log("getting doce");
    return Object.keys(data[course]);
  }
  getDataForDocument(course,document) {
    return data[course][document];
  }
}
