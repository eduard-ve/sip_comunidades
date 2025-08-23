<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="gradient-text">Sistema Integral</span>
            <br />de Información Poblacional
          </h1>
          <p class="hero-subtitle">
            Centralizando datos comunitarios para decisiones informadas y 
            fortalecimiento del territorio ancestral
          </p>
          <div class="hero-stats">
            <div class="stat-card">
              <div class="stat-number">{{ totalPopulation }}</div>
              <div class="stat-label">Habitantes Registrados</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">{{ activeFamilies }}</div>
              <div class="stat-label">Familias Activas</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">{{ lastUpdateDays }}</div>
              <div class="stat-label">Días desde última actualización</div>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="community-showcase">
            <div class="showcase-header">
              <h3>Nuestra Comunidad</h3>
              <button @click="refreshShowcase" class="refresh-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
                </svg>
              </button>
            </div>
            <div class="image-gallery">
              <div 
                v-for="(image, index) in communityImages" 
                :key="index"
                class="gallery-item"
                :class="{ active: index === activeImageIndex }"
                @click="setActiveImage(index)"
              >
                <img :src="image.url" :alt="image.description" />
                <div class="image-overlay">
                  <span>{{ image.description }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Actions Section -->
    <section class="quick-actions">
      <div class="section-header">
        <h2>Acciones Rápidas</h2>
        <p>Herramientas principales para la gestión administrativa</p>
      </div>
      <div class="actions-grid">
        <div 
          v-for="action in quickActions" 
          :key="action.id"
          class="action-card"
          @click="navigateToAction(action.route)"
        >
          <div class="action-icon" :style="{ backgroundColor: action.color }">
            <component :is="action.icon" />
          </div>
          <h3>{{ action.title }}</h3>
          <p>{{ action.description }}</p>
          <div class="action-badge">
            {{ action.count }} registros
          </div>
        </div>
      </div>
    </section>

    <!-- Community Insights -->
    <section class="insights-section">
      <div class="insights-container">
        <div class="insights-left">
          <h2>Perspectivas de la Comunidad</h2>
          <div class="insight-cards">
            <div class="insight-card">
              <div class="insight-header">
                <h4>Distribución Etaria</h4>
                <div class="insight-trend up">+2.3%</div>
              </div>
              <div class="chart-container">
                <div class="age-chart">
                  <div class="age-bar" style="height: 60%" data-age="0-15">
                    <span class="bar-label">0-15</span>
                  </div>
                  <div class="age-bar" style="height: 80%" data-age="16-35">
                    <span class="bar-label">16-35</span>
                  </div>
                  <div class="age-bar" style="height: 45%" data-age="36-55">
                    <span class="bar-label">36-55</span>
                  </div>
                  <div class="age-bar" style="height: 30%" data-age="56+">
                    <span class="bar-label">56+</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="insight-card">
              <div class="insight-header">
                <h4>Actividades Recientes</h4>
                <div class="insight-date">Últimos 7 días</div>
              </div>
              <div class="activity-list">
                <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                  <div class="activity-dot" :style="{ backgroundColor: activity.color }"></div>
                  <div class="activity-content">
                    <span class="activity-text">{{ activity.text }}</span>
                    <span class="activity-time">{{ activity.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="insights-right">
          <div class="community-map">
            <h3>Territorio Comunitario</h3>
            <div class="map-placeholder">
              <div class="map-regions">
                <div class="region" v-for="region in territoryRegions" :key="region.id">
                  <div class="region-marker" :style="{ backgroundColor: region.color }"></div>
                  <span>{{ region.name }}</span>
                  <small>{{ region.families }} familias</small>
                </div>
              </div>
              <div class="map-center">
                <div class="center-marker">
                  <div class="pulse-ring"></div>
                  <div class="center-dot"></div>
                </div>
                <span class="center-label">Centro Comunitario</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- System Status -->
    <section class="system-status">
      <div class="status-header">
        <h2>Estado del Sistema</h2>
        <div class="status-indicator" :class="systemStatus.status">
          <div class="status-dot"></div>
          <span>{{ systemStatus.message }}</span>
        </div>
      </div>
      <div class="status-grid">
        <div v-for="metric in systemMetrics" :key="metric.name" class="metric-card">
          <div class="metric-icon">
            <component :is="metric.icon" />
          </div>
          <div class="metric-info">
            <div class="metric-value">{{ metric.value }}</div>
            <div class="metric-label">{{ metric.label }}</div>
          </div>
          <div class="metric-status" :class="metric.status"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

// Router
const router = useRouter()

// Reactive data
const totalPopulation = ref(1247)
const activeFamilies = ref(312)
const lastUpdateDays = ref(2)
const activeImageIndex = ref(0)

// Community images
const communityImages = ref([
  {
    url: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop',
    description: 'Ceremonia tradicional'
  },
  {
    url: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop',
    description: 'Territorio ancestral'
  },
  {
    url: 'https://images.unsplash.com/photo-1502780402662-acc01917697e?w=400&h=300&fit=crop',
    description: 'Actividades comunitarias'
  },
  {
    url: 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400&h=300&fit=crop',
    description: 'Medicina tradicional'
  }
])

// Quick actions
const quickActions = ref([
  {
    id: 1,
    title: 'Gestión Poblacional',
    description: 'Administrar registros de habitantes',
    icon: 'UsersIcon',
    color: '#6366f1',
    route: '/poblacion',
    count: 1247
  },
  {
    id: 2,
    title: 'Reportes y Análisis',
    description: 'Generar informes estadísticos',
    icon: 'ChartBarIcon',
    color: '#8b5cf6',
    route: '/reportes',
    count: 45
  },
  {
    id: 3,
    title: 'Auditoría',
    description: 'Revisar actividades del sistema',
    icon: 'ClipboardDocumentCheckIcon',
    color: '#06b6d4',
    route: '/auditoria',
    count: 128
  },
  {
    id: 4,
    title: 'Configuración',
    description: 'Ajustes y parámetros del sistema',
    icon: 'CogIcon',
    color: '#10b981',
    route: '/configuracion',
    count: 12
  }
])

// Recent activities
const recentActivities = ref([
  {
    id: 1,
    text: 'Nuevo registro familiar agregado',
    time: 'hace 2 horas',
    color: '#10b981'
  },
  {
    id: 2,
    text: 'Actualización de datos demográficos',
    time: 'hace 5 horas',
    color: '#6366f1'
  },
  {
    id: 3,
    text: 'Reporte mensual generado',
    time: 'hace 1 día',
    color: '#8b5cf6'
  },
  {
    id: 4,
    text: 'Respaldo de datos completado',
    time: 'hace 2 días',
    color: '#06b6d4'
  }
])

// Territory regions
const territoryRegions = ref([
  { id: 1, name: 'Sector Norte', families: 89, color: '#ef4444' },
  { id: 2, name: 'Sector Sur', families: 76, color: '#f59e0b' },
  { id: 3, name: 'Sector Este', families: 92, color: '#10b981' },
  { id: 4, name: 'Sector Oeste', families: 55, color: '#6366f1' }
])

// System status
const systemStatus = ref({
  status: 'healthy',
  message: 'Todos los sistemas operativos'
})

// System metrics
const systemMetrics = ref([
  {
    name: 'database',
    label: 'Base de Datos',
    value: '99.8%',
    status: 'good',
    icon: 'CircleStackIcon'
  },
  {
    name: 'storage',
    label: 'Almacenamiento',
    value: '76%',
    status: 'good',
    icon: 'ServerIcon'
  },
  {
    name: 'backup',
    label: 'Respaldos',
    value: 'Actualizado',
    status: 'good',
    icon: 'CloudArrowUpIcon'
  },
  {
    name: 'security',
    label: 'Seguridad',
    value: 'Protegido',
    status: 'good',
    icon: 'ShieldCheckIcon'
  }
])

// Methods
const navigateToAction = (route) => {
  router.push(route)
}

const setActiveImage = (index) => {
  activeImageIndex.value = index
}

const refreshShowcase = () => {
  // Simulate refresh
  const newIndex = (activeImageIndex.value + 1) % communityImages.value.length
  setActiveImage(newIndex)
}

// Auto-rotate images
onMounted(() => {
  setInterval(() => {
    activeImageIndex.value = (activeImageIndex.value + 1) % communityImages.value.length
  }, 5000)
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #1f2937;
}

/* Hero Section */
.hero-section {
  padding: 4rem 2rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: white;
}

.gradient-text {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  color: rgba(255, 255, 255, 0.9);
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

/* Community Showcase */
.community-showcase {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.showcase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.showcase-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.refresh-btn {
  background: #6366f1;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.refresh-btn:hover {
  background: #4f46e5;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.gallery-item {
  position: relative;
  border-radius: 0.75rem;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.gallery-item:hover {
  transform: scale(1.05);
}

.gallery-item.active {
  ring: 3px solid #6366f1;
}

.gallery-item img {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
  padding: 1rem 0.75rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Quick Actions */
.quick-actions {
  padding: 4rem 2rem;
  background: white;
}

.section-header {
  max-width: 1200px;
  margin: 0 auto 3rem;
  text-align: center;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.125rem;
  color: #6b7280;
}

.actions-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.action-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--card-color);
}

.action-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
}

.action-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.action-card p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.action-badge {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
}

/* Insights Section */
.insights-section {
  padding: 4rem 2rem;
  background: #f9fafb;
}

.insights-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.insights-left h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
}

.insight-cards {
  display: grid;
  gap: 2rem;
}

.insight-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.insight-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.insight-trend {
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.insight-trend.up {
  background: #d1fae5;
  color: #065f46;
}

.insight-date {
  color: #6b7280;
  font-size: 0.875rem;
}

/* Age Chart */
.age-chart {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 120px;
}

.age-bar {
  flex: 1;
  background: linear-gradient(to top, #6366f1, #8b5cf6);
  border-radius: 0.25rem 0.25rem 0 0;
  position: relative;
  transition: all 0.3s ease;
}

.age-bar:hover {
  opacity: 0.8;
}

.bar-label {
  position: absolute;
  bottom: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.activity-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.activity-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.activity-text {
  color: #1f2937;
  font-weight: 500;
}

.activity-time {
  color: #6b7280;
  font-size: 0.875rem;
}

/* Community Map */
.community-map {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  height: fit-content;
}

.community-map h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  text-align: center;
}

.map-placeholder {
  position: relative;
  height: 300px;
  background: #f3f4f6;
  border-radius: 0.75rem;
  overflow: hidden;
}

.map-regions {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.region {
  background: rgba(255, 255, 255, 0.9);
  padding: 0.75rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.region-marker {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}

.region span {
  font-weight: 500;
  color: #1f2937;
}

.region small {
  color: #6b7280;
  margin-left: auto;
}

.map-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.center-marker {
  position: relative;
  width: 3rem;
  height: 3rem;
  margin: 0 auto 0.5rem;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid #6366f1;
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.center-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1rem;
  height: 1rem;
  background: #6366f1;
  border-radius: 50%;
}

.center-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
}

/* System Status */
.system-status {
  padding: 4rem 2rem;
  background: white;
}

.status-header {
  max-width: 1200px;
  margin: 0 auto 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-weight: 500;
}

.status-indicator.healthy {
  background: #d1fae5;
  color: #065f46;
}

.status-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  background: currentColor;
}

.status-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.metric-icon {
  width: 3rem;
  height: 3rem;
  background: #f3f4f6;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.metric-info {
  flex: 1;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.metric-status {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}

.metric-status.good {
  background: #10b981;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .insights-container {
    grid-template-columns: 1fr;
  }
  
  .status-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-stats {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .image-gallery {
    grid-template-columns: 1fr;
  }
  
  .map-regions {
    grid-template-columns: 1fr;
  }
}
</style>