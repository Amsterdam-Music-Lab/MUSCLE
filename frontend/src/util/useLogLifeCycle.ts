import { useEffect } from "react";

export default function useLogLifeCycle(
  name: string,
  logEffects: boolean = false
) {
  console.log(`${name} mounted`);
  useEffect(() => {
    if (logEffects) console.log(`${name} mounted (effect)`);
    return () => console.log(`* ${name} unmounted`);
  }, []);
}
