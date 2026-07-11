import { useEffect, useState } from "react";

export default function CountUp({
  end,
  duration = 1000,
  decimals = 0
}) {

    const [count, setCount] = useState(0);

    useEffect(() => {

        let start = 0;

        const increment = end / (duration / 16);

        const timer = setInterval(() => {

            start += increment;

            if (start >= end) {

                setCount(end);

                clearInterval(timer);

            } else {

                setCount(Number(start.toFixed(decimals)));

            }

        },16);

        return () => clearInterval(timer);
        
        return count.toLocaleString(undefined,{
  minimumFractionDigits:decimals,
  maximumFractionDigits:decimals
});

    },[end,duration]);

    return count;
}