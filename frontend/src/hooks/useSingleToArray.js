import { useState, useEffect } from "react";

const useSingleToArray = (single)=>{
  const [array, setArray] = useState([single]);
  useEffect(() => {
      setArray([single]);
  }, [single]);

  return array;
}

export default useSingleToArray;

