import data from './data.json';

const courses = Object.keys(data)
export default class Data {
  getCourses() {
    return courses.filter(course => data[course].length > 0 );
  }
  getDataForCourse(course) {
    return data[course];
  }
}
