import { Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>Технологии</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="Технологии" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Backend</h2>
          <ul className={styles.list}>
            <li className={styles.textItem}>Python 3.12</li>
            <li className={styles.textItem}>Django</li>
            <li className={styles.textItem}>Django REST Framework</li>
            <li className={styles.textItem}>Djoser — аутентификация по токену</li>
            <li className={styles.textItem}>PostgreSQL 15</li>
            <li className={styles.textItem}>Pillow — обработка изображений</li>
          </ul>

          <h2 className={styles.subtitle}>Frontend</h2>
          <ul className={styles.list}>
            <li className={styles.textItem}>React</li>
            <li className={styles.textItem}>React Router</li>
            <li className={styles.textItem}>CSS Modules</li>
          </ul>

          <h2 className={styles.subtitle}>Инфраструктура</h2>
          <ul className={styles.list}>
            <li className={styles.textItem}>Docker, Docker Compose</li>
            <li className={styles.textItem}>Nginx</li>
            <li className={styles.textItem}>GitHub Actions — CI/CD</li>
            <li className={styles.textItem}>Docker Hub — хранение образов</li>
            <li className={styles.textItem}>Let's Encrypt — SSL-сертификаты</li>
          </ul>
        </div>
      </div>
      
    </Container>
  </Main>
}

export default Technologies