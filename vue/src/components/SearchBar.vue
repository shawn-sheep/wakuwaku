<template>
  <div class="search-div">
    <svg width="24" height="24" stroke="CurrentColor" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 38C30.3888 38 38 30.3888 38 21C38 11.6112 30.3888 4 21 4C11.6112 4 4 11.6112 4 21C4 30.3888 11.6112 38 21 38Z" fill="none" stroke-width="4" stroke-linejoin="round"/><path d="M26.657 14.3431C25.2093 12.8954 23.2093 12 21.0001 12C18.791 12 16.791 12.8954 15.3433 14.3431" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M33.2216 33.2217L41.7069 41.707" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <input>
  </div>
</template>

<script>
export default {
  name: "SearchBar"
}
</script>

<style scoped>
.search-div {
  width: 100%;
  height: 30px;
  position: relative;
  background: var(--wakuwaku-searchbar-background-color);
  border-radius: 999px;
  display: flex;
  flex-direction: row;
}

input {
  position: relative;
  width: calc(100% - 30px);
  height: 100%;
  background-color: rgba(0,0,0,0);
  border: none;
  margin: auto;
  color: inherit;
  font-family: inherit;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.25px;
  z-index: 100;
  top: -0.5px;
}
input:focus-visible {
  outline: none;
}
svg {
  width: 20px;
  height: 20px;
  padding-left: 10px;
  padding-right: 5px;
}
</style>
