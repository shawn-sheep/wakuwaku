<link rel="stylesheet" href="assets/font/Inter Web/inter.css">
<template>
  <div>
    <router-view/>
    <keep-alive>
      <waku-image-detail></waku-image-detail>
    </keep-alive>
  </div>
</template>

<style>
#app {
  /*font-family: 'Inter',Avenir, Helvetica, Arial, sans-serif;*/
  font-family: 'Inter';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: 14px;
  --wakuwaku-background-color: #FFE4E1;
  --wakuwaku-main-background-color: white;
  --wakuwaku-header-background-color: #FFE4E1;
  --wakuwaku-header-font-color: #E8948B;
  --wakuwaku-header-hover-color: #d08882;
  --wakuwaku-color: #FFF0F5;
  --wakuwaku-color-light: #FFF8FB;
  --wakuwaku-color-lighter: #fffcfd;
  --wakuwaku-color-dark: #FFE1ED;
  --wakuwaku-font-color: #B39EA5;
  --wakuwaku-font-color-dark: #665A5E;
  --wakuwaku-color-spring-grean: #00CD66;
  --wakuwaku-large-radius: 8px;
  --wakuwaku-medium-radius: 5px;
  --wakuwaku-searchbar-background-color: #FFFFFF;
  --wakuwaku-searchbar-border-color: #eab3ad;
  --wakuwaku-searchbar-hover-background-color: #fcecea;
  --wakuwaku-scrollbar-color: #FFE4E1;
  --wakuwaku-scrollbar-thumb-color: #eab3ad;
  --wakuwaku-user-bar-height: 400px;
  --wakuwaku-artist-tag-color: #dd0000;
  --wakuwaku-copy-right-tag-color: #a800aa;
  --wakuwaku-character-tag-color: #00ab2c;
  --wakuwaku-general-tag-color: #0075f8;
  --wakuwaku-meta-tag-color: #fd9200;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

body {
  margin: 0;
  user-select: none;
}

.fade-enter-active {
  animation: fade 0.2s;
}

.fade-leave-active {
  animation: fade 0.2s reverse;
}

.shrink-enter-active {
  animation: expand 0.2s;
}

.shrink-leave-active {
  animation: shrink 0.2s;
}

@keyframes fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes shrink {
  from {
    scale: 1.2;
  }
  to {
    scale: 1;
  }
}

@keyframes expand {
  from {
    scale: 1;
  }
  to {
    scale: 1.2;
  }
}

.pull-down-enter-active {
  animation: pull-down 0.2s;
}

.pull-down-leave-active {
  animation: pull-down 0.2s reverse;
}

@keyframes pull-down {
  from {
    height: 0;
  }
  to {
    height: var(--wakuwaku-user-bar-height);
  }
}

.spinner-5 {
  width: 50px;
  --b: 8px; /* the border thickness */
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--wakuwaku-header-font-color);
  -webkit-mask:
      repeating-conic-gradient(#0000 0deg,#000 1deg 70deg,#0000 71deg 90deg),
      radial-gradient(farthest-side,#0000 calc(100% - var(--b) - 1px),#000 calc(100% - var(--b)));
  -webkit-mask-composite: destination-in;
  mask-composite: intersect;
  animation: s5 1s infinite;
}
@keyframes s5 {to{transform: rotate(.5turn)}}


</style>
<script>
import WakuImageDetail from "@/components/WakuImageDetail";
export default {
  components: {WakuImageDetail}
}
</script>
