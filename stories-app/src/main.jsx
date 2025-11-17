import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter,RouterProvider } from 'react-router-dom'
import DetailStory from '../src/Pages/Stories/detail-story.jsx'
import LunchStory from '../src/Pages/Stories/lunch-story.jsx'
import FormElements from './Pages/Admin/Forms/FormElements.Jsx'

// const router=createBrowserRouter([
//   {
//     path:"/storyDetail",element:<DetailStory/>
//   },
//   {    path:"/lunchStory",element:<LunchStory/>
//   },
//   // {
//   //   path:"/admin/addStory",element:<FormElements/>
//   // }
// ])
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App/>
  </StrictMode>,
)
