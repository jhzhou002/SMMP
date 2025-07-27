import { Router } from 'express'
import { ProjectController } from '../controllers/ProjectController'

const router = Router()
const projectController = new ProjectController()

router.post('/', (req, res) => projectController.createProject(req, res))
router.get('/', (req, res) => projectController.getProjects(req, res))
router.get('/:id', (req, res) => projectController.getProject(req, res))
router.get('/:id/status', (req, res) => projectController.getProjectStatus(req, res))
router.get('/:id/files', (req, res) => projectController.getProjectFiles(req, res))

export default router