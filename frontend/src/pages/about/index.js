import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>О проекте</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что это за сайт?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Foodgram — это платформа для публикации рецептов, подписки на авторов и формирования списка покупок. Проект создан в рамках обучения в Яндекс Практикуме и представляет собой полноценное веб-приложение с backend на Django и frontend на React.
            </p>
            <p className={styles.textItem}>
              Пользователи могут создавать рецепты с ингредиентами и тегами, загружать изображения блюд, добавлять чужие рецепты в избранное и корзину. Отдельная функция — скачивание сводного списка покупок в текстовом формате, который формируется автоматически из всех рецептов в корзине.
            </p>
            <p className={styles.textItem}>
              Также реализована система подписок: можно подписаться на других авторов и следить за их новыми рецептами. Все рецепты фильтруются по тегам, автору, избранному и списку покупок.
            </p>
            <p className={styles.textItem}>
              Чтобы использовать все возможности сайта — нужна регистрация. Проверка адреса электронной почты не осуществляется, вы можете ввести любой email.
            </p>
            <p className={styles.textItem}>
              Заходите и делитесь своими любимыми рецептами!
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Код проекта находится тут — <a href="https://github.com/Kirullk/foodgram" className={styles.textLink}>GitHub</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="https://t.me/kiyrer" className={styles.textLink}>kiyrer</a>
            </p>
          </div>
        </aside>
      </div>
      
    </Container>
  </Main>
}

export default About