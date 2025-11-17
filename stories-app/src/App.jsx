import { Parallax, ParallaxLayer } from "@react-spring/parallax";
import {Route,Routes,BrowserRouter} from "react-router-dom"
import LunchStory from "../src/Pages/Stories/lunch-story";
import FormElements from "./Pages/Admin/Forms/FormElements.Jsx";
import AdminLayout from "./Pages/Admin/Layout/admin-layout";
import AddUserForm from "./Pages/Admin/users/addUser";
import AddStoryForm from "./Pages/Admin/Stories/addStory";

export default function App() {
 return(

   <BrowserRouter>
      <Routes>
        <Route path="/admin" element={<AdminLayout />}>
          <Route path="addStory" element={<AddStoryForm />} />
          <Route path="viewAllStories" element={<FormElements />} />
          <Route path="addUser" element={<AddUserForm />} />
          <Route path="viewAllUsers" element={<FormElements />} />
          <Route path="addGenre" element={<FormElements />} />
          <Route path="viewAllGenre" element={<FormElements />} />
        </Route>
      </Routes>
    </BrowserRouter>

  );
}
