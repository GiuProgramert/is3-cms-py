import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { clearStates } from "../reducers/Alert"

export const Alert = () => {
    const dispatch=useDispatch()
    const {isOk,isError,error,message}=useSelector((state)=>{return state.Alert})
    useEffect(() => {
      if (isError || isOk) {
        const tiempo = setTimeout(() => {
          dispatch(clearStates());
        }, 3000);
        return () => {
          clearTimeout(tiempo);
        };
      }
    }, [isError,isOk])
    return (
      <>
          {isOk &&
              <div className="alerts" style={{ "marginBottom": "10px" }}>
                <div className="alert alert-dismissible fade show alert-success" role="alert" data-mdb-color="success" id="alert-success">
                  <strong>{message}</strong>
                  <button type="button" className="btn-close" data-mdb-dismiss="alert" aria-label="Close"></button>
                </div>
              </div>
            }
            {isError &&
              <div className="alerts" style={{ "marginBottom": "10px" }}>
                <div className="alert alert-dismissible fade show alert-danger" role="alert" data-mdb-color="error" id="alert-success">
                  <strong>{error}</strong>
                  <button type="button" className="btn-close" data-mdb-dismiss="alert" aria-label="Close"></button>
                </div>
              </div>
            }     
      </>
    )
  }