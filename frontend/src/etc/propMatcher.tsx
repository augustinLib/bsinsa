export type propMatcherProps = {
  "": string;
  hood: string;
  knit: string;
  long: string;
  polo: string;
  shirt: string;
  short: string;
  sleeveless: string;
  sweat: string;
  cotton: string;
  denim: string;
  jogger: string;
  jumper: string;
  leggings: string;
  shorts: string;
  slacks: string;
  etc: string;
};

export interface ItemProps {
  hood: number[];
  knit: number[];
  long: number[];
  polo: number[];
  shirt: number[];
  short: number[];
  sleeveless: number[];
  sweat: number[];
  cotton: number[];
  denim: number[];
  jogger: number[];
  jumper: number[];
  leggings: number[];
  shorts: number[];
  slacks: number[];
  etc: number[];
}

export const propMatcher: propMatcherProps = {
  "": "BSINSA",
  hood: "후드",
  knit: "니트",
  long: "롱슬리브",
  polo: "폴로",
  shirt: "셔츠",
  short: "티셔츠",
  sleeveless: "민소매",
  sweat: "스웨터",
  cotton: "면바지",
  denim: "청바지",
  jogger: "조거팬츠",
  jumper: "점퍼",
  leggings: "레깅스",
  shorts: "반바지",
  slacks: "슬랙스",
  etc: "기타 바지",
};

export const emptyProps = {
  hood: [],
  knit: [],
  long: [],
  polo: [],
  shirt: [],
  short: [],
  sleeveless: [],
  sweat: [],
  cotton: [],
  denim: [],
  jogger: [],
  jumper: [],
  leggings: [],
  shorts: [],
  slacks: [],
  etc: [],
};

export default propMatcher;
