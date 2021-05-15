import React, { useState } from 'react';
import './App.css';
import Form1 from './components/forms/form1';
import Simulator from './components/simulation';
import { useDispatch, useSelector } from "react-redux";
import { AppState } from "./redux/stores/renderer";


import { makeStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > * + *': {
      marginLeft: theme.spacing(2),
    },
  },
}));


function App() {
  const classes = useStyles();
  const { isLoading } = useSelector(
    (state: AppState) => state.commonProps
  );
  const [state, setState] = useState({})
  const [flag, setFlag] = useState(false);
  const setGlobalVariabels = (subVars: any) => {
    setState({ ...state, ...subVars })
    setFlag(true);
  }
  const onMain = (e: any) => {
    console.log(e);
    setFlag(false);
  }


  return (
    <div className="App">
      {
        isLoading === true ?
          <div className={classes.root}>
            <CircularProgress />
          </div> :
          <div className="App">
            {
              flag === false ?
                <Form1
                  setVariabels={setGlobalVariabels}
                ></Form1> :
                <Simulator
                  setFlag={onMain}
                ></Simulator>
            }
          </div >
      }
    </div>
  );
}

export default App;
