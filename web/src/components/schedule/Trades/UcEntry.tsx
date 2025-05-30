import axios from "axios";
import { useEffect, useState } from "react";
import { IoIosArrowDown } from "react-icons/io";

export default function UcEntry({
  shift,
  uc,
  type_class,
  setShiftTrade,
}: {
  shift: string;
  uc: string;
  type_class: string;
  setShiftTrade: React.Dispatch<
    React.SetStateAction<
      {
        uc: string;
        type_class: string;
        shift: string;
        shiftBeforeTrade: string;
      }[]
    >
  >;
}) {
  const startShift = type_class + shift;

  const [isOpen, setIsOpen] = useState(false);
  const [currentShift, setCurrentShift] = useState(startShift);
  const [shifts, setShifts] = useState([]);

  useEffect(() => {
    const params = { uc: uc, type_class: type_class };

    axios
      .get("api/trade/shifts", { params: params })
      .then((response) => {
        console.log(response)
        setShifts(response.data.shifts);
      })
      .catch((error) => console.log(error));
  }, [axios, type_class, uc]);

  function handleClick(shiftBeforeTrade: string, shift: string) {
    setShiftTrade((shiftTrade) => [
      ...shiftTrade.filter(
        (element) =>
          element.uc !== uc && element.type_class.slice(0, -1) !== type_class
      ),
      {
        uc: uc,
        type_class: type_class,
        shift: shift,
        shiftBeforeTrade: shiftBeforeTrade,
      },
    ]);
  }

  return (
    <div className="z-10 flex bg-blue-500 hover:bg-blue-600 hover:duration-300 w-full h-auto mt-2 pb-2 rounded-3xl">
      <div className="p-2 ml-1 top-1/2 left-1/2 w-5/6">
        <p className="font-semibold text-sm text-white">
          {uc + " - " + currentShift}
        </p>
      </div>
      <div className="relative">
        <button
          onClick={() => {
            setIsOpen(!isOpen);
          }}
        >
          <IoIosArrowDown className="z-20 font-semibold text-white mt-3 ml-6" />
        </button>
        <div
          className={`${
            isOpen ? "" : "hidden"
          } z-30 absolute bg-white rounded border border-gray-200`}
        >
          {shifts.map((shift, index) => {
            return (
              <button
                key={index}
                onClick={() => {
                  const shiftBeforeTrade = currentShift;
                  setIsOpen(!isOpen);
                  setCurrentShift(shift);
                  handleClick(shiftBeforeTrade, shift);
                }}
                className="block text-sm text-black px-3 pb-1 pt-1 h-6 bg-gray-100 hover:bg-gray-300"
              >
                {shift}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
