import data from './data.json';

const courses = Object.keys(data)
export default class Data {
  getCourses() {
    return courses;
  }
  getDataForCourse(course) {
    return data[course];
  }
}
