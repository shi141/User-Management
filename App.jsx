import React, { useState, useEffect } from 'react';
import {getdataa} from '../src/new.ts';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
// import "./App.css";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import styled from 'styled-components';
import { deepOrange, green } from '@mui/material/colors';
import { useNavigate } from 'react-router-dom';
import SimpleDialog from './components/dialog.tsx';
import SimpleDialog1 from './components/edit.tsx';


// const MyButton = styled(Button)`
//   background-color: red;
//   margin-left: 70%;
//   padding: 15px;
// `;

export default function Home() {
  const [data, setData] = useState([]);
  const[openDialog1,setOpenDialog1] = useState(false);
  const[openDialog2,setOpenDialog2] = useState(false);
  const[selectedUser,setSelectedUser]=useState(null);
  const[selectedData,setSelectedData]=useState(null);
  const [dataLoaded, setDataLoaded] = useState(false);

  useEffect(() => {
    const fetchdata=async()=>{
      const fetcheddata=await getdataa();
      setData(fetcheddata);
    };

    fetchdata();
    
  }, []);

  const handleDelete = async (id,data) => {
        if(confirm("Are you sure you want to delete ?")){
          const new_arr=[...data];
          const index=new_arr.findIndex(i=>i.id===id);
          const response = await fetch(`http://127.0.0.1:80/delete_user/${id}`, {
            method: 'DELETE',
          });
          if (response.ok) {
            const result = await response.json();
            new_arr.splice(index,1);
            setData(new_arr);
            // if (result){
            //   alert("user deleted succesfully");
            // }
            alert("user deleted succesfully");
            // window.location.reload(); // Alert success message
          } else {
            alert('Failed to add user');
          }
        }
        else{
          console.log('deletion cancelled');
        }
        

  };
  const handleEditClick = (user,data) => {
    
    setSelectedData(data);
    setSelectedUser(user);// Store the user object for editing
    setOpenDialog2(true); // Open edit dialog
  };
const handleAddUser=()=>{
  setOpenDialog1(true);
  setData(data);
  setDataLoaded(true);
}
  
 return (

  <div>
    <div>
    <Button onClick={()=>handleAddUser()} variant="contained" sx={{bgcolor:deepOrange,fontSize:"lrem",marginLeft:"90%"}} >
  + Add User
</Button>
{openDialog1 && dataLoaded && <SimpleDialog open={openDialog1} data={data} setdata={setData} setdialog={setOpenDialog1}  />}
</div>
    <TableContainer component={Paper} sx={{marginTop:"5%"}}>
    <Table sx={{ minWidth: 650 }} aria-label="simple table">
      <TableHead>
        <TableRow>
          <TableCell>ID</TableCell>
          <TableCell>NAME</TableCell>
          <TableCell>DEPARTMENT</TableCell>
          <TableCell>EMAIL</TableCell>
          <TableCell>ROLE</TableCell>
          <TableCell>CONTACT</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map((item,index)=>(
        <TableRow key={index}>
          <TableCell>{item.id}</TableCell>
          <TableCell>{item.name}</TableCell>
          <TableCell>{item.department}</TableCell>
          <TableCell>{item.email}</TableCell>
          <TableCell>{item.role}</TableCell>
          <TableCell>{item.contact}</TableCell>

          <TableCell><Button onClick={()=>handleEditClick(item,data)} variant="text" sx={{color:green[700],fontSize:"lrem"}} >Edit</Button>
          {/* {openDialog2 && <SimpleDialog1 open={openDialog2} />} */}
          </TableCell>
          {openDialog2 && (
                <SimpleDialog1
                  open={openDialog2}
                  user={selectedUser}
                  data={selectedData}
                  setdata={setData}
                  setdialog={setOpenDialog2}
                   // Pass update function as a prop
                  onClose={() => setOpenDialog2(false)}
                />
              )}
          <TableCell><Button onClick={()=>handleDelete(item.id,data)} variant="text" sx={{color:"red",fontSize:"lrem"}} >Delete</Button>
          {/* {openDialog2 && <SimpleDialog1 open={openDialog2} />} */}
          </TableCell>
        </TableRow>))}
      </TableBody>
    </Table>
    </TableContainer>

  </div>
 );
}





// import React from 'react';
// import Sidebar from './components/sidebar';
// import Sidebar from './components/content';
// import Sidebar from './components/Profile';

// import './App.css';

// const App=()=>{
//   return <div className='dashboard'>
//     <Sidebar />
//     <div className="dashboard--content">
//       <Content />
//       <Profile/>
//     </div>
//   </div>;
  
// }
// export default App;