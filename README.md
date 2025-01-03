curl --location 'http://localhost:8000/pets/register/' \
--form 'file=@/Users/gabriel.cerioni/PycharmProjects/gabsPetFinder/app/services/bart_shiba.jpg' \
--form 'pet_metadata={
  "name": "Bart",
  "species": "dog",
  "breed": "Shiba Inu",
  "age": 5,
  "color": "orange-white",
  "owner_name": "Gabriel Cerioni",
  "owner_contact": "+55 11 98765-4321",
  "last_known_location": "-23.567890,-46.654321",
  "city": "São Paulo",
  "state": "SP"
}'


 curl --location 'http://localhost:8000/pets/register/' \
--form 'file=@/Users/gabriel.cerioni/PycharmProjects/gabsPetFinder/app/services/bruce_bulldog.jpg' \
--form 'pet_metadata={
  "name": "Bruce",
  "species": "dog",
  "breed": "Bulldog",
  "age": 4,
  "color": "black and white",
  "owner_name": "Leslie Cavazzana",
  "owner_contact": "+55 11 91234-5678",
  "last_known_location": "-23.568900,-46.655432",
  "city": "São Paulo",
  "state": "SP"
}'


curl --location 'http://localhost:8000/pets/register/' \
--form 'file=@/Users/gabriel.cerioni/PycharmProjects/gabsPetFinder/app/services/stella_maltese.jpg' \
--form 'pet_metadata={
  "name": "Stella Artois",
  "species": "dog",
  "breed": "Maltese",
  "age": 3,
  "color": "white",          
  "owner_name": "Poliana Proni",   
  "owner_contact": "+55 11 98765-4321",
  "last_known_location": "-23.567001,-46.654123",
  "city": "São Paulo",
  "state": "SP"
}'
